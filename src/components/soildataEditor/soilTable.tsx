import React, { useContext, useState } from "react";
import { Column, EditableCell, Table, TableLoadingOption } from "@blueprintjs/table";

import EditableTableContext from "../../editableTableContext";
import { Intent } from "@blueprintjs/core";
import { setCells } from "../../actions/editableTableAction";

const DEFAULT_COLUMN_NAME = ["深度", "N値", "土質", "低減係数", "α", "E0"]


const SoilTable = (props: {columnWidth: number, numRows: number}) => {

  const { state, dispatch } = useContext(EditableTableContext);
  const [sparseCellIntent, setSparseCellIntent] = useState({} as { [key: string]: Intent; });

  const dataKey = (rowIndex: number, columnIndex: number) => {
    return `${rowIndex}-${columnIndex}`;
  };

  function isValidValue(value: string, columnIndex: number) {
    if (columnIndex === 2) {  // 土質
      return /^(S|C)$/.test(value);
    } if (columnIndex === 5) {  // alpha
      return /^(8|6)0$/.test(value);
    } else {
      return /^[0-9.]*$/.test(value);  // その他
    }
  }

  function cellValidator(rowIndex: number, columnIndex: number) {
    const key = dataKey(rowIndex, columnIndex);
    return (value: string) => {
      setSparseCellIntent(() => {
        sparseCellIntent[key] = isValidValue(value, columnIndex) ? "none" : Intent.DANGER;
        return sparseCellIntent
      });
      // dispatch(setCells({[key]: value}));
    };
  };

  function cellSetter(rowIndex: number, columnIndex: number) {
    const key = dataKey(rowIndex, columnIndex);
    return (value: string) => {
      dispatch(setCells({[key]: value}));
    };
  };

  const renderCell = (rowIndex: number, columnIndex: number) => {
    const key = dataKey(rowIndex, columnIndex);
    const value = state.tableData.sparseCellData![key];
    return (
      <EditableCell
        value={value == null ? "" : value}
        intent={sparseCellIntent[key]}
        onCancel={cellValidator(rowIndex, columnIndex)}
        onChange={cellValidator(rowIndex, columnIndex)}
        onConfirm={cellSetter(rowIndex, columnIndex)}
      />
    );
  };

  function getLoadingOptions() {
    const loadingOptions: TableLoadingOption[] = [];
    if (state.tableData.cellsLoading) {
      loadingOptions.push(TableLoadingOption.CELLS);
    }
    return loadingOptions;
  }

  const columns = DEFAULT_COLUMN_NAME.map((_: string, index: number) => {
    return (
      <Column key={index} name={DEFAULT_COLUMN_NAME[index]} cellRenderer={renderCell} />
    );
  });

  return (
    <Table
      enableColumnResizing={false}
      enableRowResizing={false}
      defaultColumnWidth={props.columnWidth}
      numRows={props.numRows}
      loadingOptions={getLoadingOptions()}>
      {columns}
    </Table>
  );
};

export default SoilTable;
