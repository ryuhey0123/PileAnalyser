import React, { useContext } from "react";

import { Intent } from "@blueprintjs/core";
import { Column, EditableCell, Table, TableLoadingOption } from "@blueprintjs/table";
import Context from "../Context";

const SoildataTable = () => {
    const dataKey = (rowIndex: number, columnIndex: number) => {
        return `${rowIndex}-${columnIndex}`;
    };

    const { state, dispatch } = useContext(Context)

    // public async componentDidMount() {
    //     const res = await fetch("/upload", { method: "POST" });
    //     const data = await res.json();
    //     return this.setState({ sparseCellData: data.data, cellsLoading: false });
    // };

    const columns = state.soildata.columnNames.map((_: string, index: number) => {
            return (
                <Column key={index} name={state.soildata.columnNames[index]} cellRenderer={renderCell} />
            );
        });


    const renderCell = (rowIndex: number, columnIndex: number) => {
        const key = dataKey(rowIndex, columnIndex);
        const value = state.soildata.sparseCellData![key];
        return (
            <EditableCell
                value={value == null ? "" : value}
                intent={state.soildata.sparseCellIntent[key]}
                onCancel={cellValidator(rowIndex, columnIndex)}
                onChange={cellValidator(rowIndex, columnIndex)}
                onConfirm={cellSetter(rowIndex, columnIndex)}
            />
        );
    };

    function isValidValue(value: string, columnIndex: number) {
        if (columnIndex === 2) {  // 土質
            return /^(S|C)$/.test(value);
        } if (columnIndex === 5) {  // alpha
            return /^(8|6)0$/.test(value);
        } else {
            return /^[0-9.]*$/.test(value);
        }
    }

    const cellValidator = (rowIndex: number, columnIndex: number) => {
        const key = dataKey(rowIndex, columnIndex);
        return (value: string) => {
            const intent = isValidValue(value, columnIndex) ? null : Intent.DANGER;
            setSparseState("sparseCellIntent", key, intent);
            setSparseState("sparseCellData", key, value);
        };
    };

    const cellSetter = (rowIndex: number, columnIndex: number) => {
        const key = dataKey(rowIndex, columnIndex);
        return (value: string) => {
            const intent = isValidValue(value, columnIndex) ? null : Intent.DANGER;
            setSparseState("sparseCellData", key, value);
            setSparseState("sparseCellIntent", key, intent);
        };
    };

    function setSparseState<T>(stateKey: string, dataKey: string, value: T) {
        const stateData = (state.soildata as any)[stateKey] as { [key: string]: T };
        const values = { ...stateData, [dataKey]: value };
        // setState({ [stateKey]: values });
    }

    function getLoadingOptions() {
        const loadingOptions: TableLoadingOption[] = [];
        if (state.soildata.cellsLoading) {
            loadingOptions.push(TableLoadingOption.CELLS);
        }
        return loadingOptions;
    }

    return (
        <Table
            enableColumnResizing={false}
            enableRowResizing={false}
            defaultColumnWidth={80}
            numRows={32}
            loadingOptions={getLoadingOptions()}
        >
        {columns}
        </Table>
    );
};

export default SoildataTable;


export interface IEditableTableState {
    columnNames?: string[];
    sparseCellData?: { [key: string]: string };
    sparseCellIntent?: { [key: string]: Intent };
    sparseColumnIntents?: Intent[];
    cellsLoading?: boolean;
}

export class EditableTable extends React.PureComponent<IEditableTableState> {
    public static dataKey = (rowIndex: number, columnIndex: number) => {
        return `${rowIndex}-${columnIndex}`;
    };

    public state: IEditableTableState = {
        columnNames: ["深度", "N値", "土質", "低減係数", "採用低減係数", "α", "E0"],
        sparseCellData: {},
        sparseCellIntent: {},
        sparseColumnIntents: [],
        cellsLoading: true,
    };

    public async componentDidMount() {
        const res = await fetch("/upload", { method: "POST" });
        const data = await res.json();
        return this.setState({ sparseCellData: data.data, cellsLoading: false });
    };

    public render() {
        const columns = this.state.columnNames!.map((_: string, index: number) => {
            return (
                <Column key={index} name={this.state.columnNames![index]} cellRenderer={this.renderCell} />
            );
        });
        return (
                <Table
                    enableColumnResizing={false}
                    enableRowResizing={false}
                    defaultColumnWidth={80}
                    numRows={32}
                    loadingOptions={this.getLoadingOptions()}
                >
                {columns}
                </Table>
        );
    }

    public renderCell = (rowIndex: number, columnIndex: number) => {
        const dataKey = EditableTable.dataKey(rowIndex, columnIndex);
        const value = this.state.sparseCellData![dataKey];
        return (
            <EditableCell
                value={value == null ? "" : value}
                intent={this.state.sparseCellIntent![dataKey]}
                onCancel={this.cellValidator(rowIndex, columnIndex)}
                onChange={this.cellValidator(rowIndex, columnIndex)}
                onConfirm={this.cellSetter(rowIndex, columnIndex)}
            />
        );
    };

    private isValidValue(value: string, columnIndex: number) {
        if (columnIndex === 2) {  // 土質
            return /^(S|C)$/.test(value);
        } if (columnIndex === 5) {  // alpha
            return /^(8|6)0$/.test(value);
        } else {
            return /^[0-9.]*$/.test(value);
        }
    }

    private cellValidator = (rowIndex: number, columnIndex: number) => {
        const dataKey = EditableTable.dataKey(rowIndex, columnIndex);
        return (value: string) => {
            const intent = this.isValidValue(value, columnIndex) ? null : Intent.DANGER;
            this.setSparseState("sparseCellIntent", dataKey, intent);
            this.setSparseState("sparseCellData", dataKey, value);
        };
    };

    private cellSetter = (rowIndex: number, columnIndex: number) => {
        const dataKey = EditableTable.dataKey(rowIndex, columnIndex);
        return (value: string) => {
            const intent = this.isValidValue(value, columnIndex) ? null : Intent.DANGER;
            this.setSparseState("sparseCellData", dataKey, value);
            this.setSparseState("sparseCellIntent", dataKey, intent);
        };
    };

    private setSparseState<T>(stateKey: string, dataKey: string, value: T) {
        const stateData = (this.state as any)[stateKey] as { [key: string]: T };
        const values = { ...stateData, [dataKey]: value };
        this.setState({ [stateKey]: values });
    }

    private getLoadingOptions() {
        const loadingOptions: TableLoadingOption[] = [];
        if (this.state.cellsLoading) {
            loadingOptions.push(TableLoadingOption.CELLS);
        }
        return loadingOptions;
    }
}
