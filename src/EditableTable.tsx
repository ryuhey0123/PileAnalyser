import * as React from "react";

import { Intent } from "@blueprintjs/core";
import { Column, EditableCell, Table, TableLoadingOption } from "@blueprintjs/table";

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
                    defaultColumnWidth={75}
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
