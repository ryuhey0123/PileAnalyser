import React, { useContext, useEffect } from "react";
import { Column, EditableCell, Table, TableLoadingOption } from "@blueprintjs/table";

import Context from "../context";
import { cellLoading, cellSetter, cellValidator } from "../actions/actionCreator";

const SoildataTable = () => {
    const dataKey = (rowIndex: number, columnIndex: number) => {
        return `${rowIndex}-${columnIndex}`;
    };

    const { state, dispatch } = useContext(Context)

    useEffect(()=> {
        fetch("/upload", { method: "POST" })
        .then(res => res.json())
        .then(data => cellLoading(data.data, false, dispatch))
    }, [dispatch]);

    const renderCell = (rowIndex: number, columnIndex: number) => {
        const key = dataKey(rowIndex, columnIndex);
        const value = state.soildata.sparseCellData![key];
        return (
            <EditableCell
                value={value == null ? "" : value}
                intent={state.soildata.sparseCellIntent![key]}
                onCancel={cellValidator(rowIndex, columnIndex, dispatch)}
                onChange={cellValidator(rowIndex, columnIndex, dispatch)}
                onConfirm={cellSetter(rowIndex, columnIndex, dispatch)}
            />
        );
    };

    function getLoadingOptions() {
        const loadingOptions: TableLoadingOption[] = [];
        if (state.soildata.cellsLoading) {
            loadingOptions.push(TableLoadingOption.CELLS);
        }
        return loadingOptions;
    }

    const columns = state.soildata.columnNames!.map((_: string, index: number) => {
        return (
            <Column key={index} name={state.soildata.columnNames![index]} cellRenderer={renderCell} />
        );
    });

    return (
        <Table
            enableColumnResizing={false}
            enableRowResizing={false}
            defaultColumnWidth={80}
            numRows={32}
            loadingOptions={getLoadingOptions()}>
        {columns}
        </Table>
    );
};

export default SoildataTable;
