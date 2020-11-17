/*
 * Copyright 2016 Palantir Technologies, Inc. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import * as React from "react";

import { Intent } from "@blueprintjs/core";
import { Column, EditableCell, Table } from "@blueprintjs/table";

export interface ITableEditableExampleState {
    columnNames?: string[];
    rowNum?: number;
    sparseCellData?: { [key: string]: string };
    sparseCellIntent?: { [key: string]: Intent };
    sparseColumnIntents?: Intent[];
}

export class TableEditableExample extends React.PureComponent<ITableEditableExampleState> {
    public static dataKey = (rowIndex: number, columnIndex: number) => {
        return `${rowIndex}-${columnIndex}`;
    };

    public state: ITableEditableExampleState = {
        columnNames: ["深度", "N値", "土質", "低減係数", "採用低減係数", "α", "E0"],
        rowNum: 1,
        sparseCellData: {},
        sparseCellIntent: {},
        sparseColumnIntents: [],
    };

    public async componentDidMount() {
        const res = await fetch("/upload", { method: "POST" });
        const data = await res.json();
        return this.setState({ rowNum: data.row_num, sparseCellData: data.data });
    };

    public render() {
        const columns = this.state.columnNames!.map((_: string, index: number) => {
            return (
                <Column key={index} name={this.state.columnNames![index]} cellRenderer={this.renderCell} />
            );
        });
        return (
                <Table numRows={this.state.rowNum}>{columns}</Table>
        );
    }

    public renderCell = (rowIndex: number, columnIndex: number) => {
        const dataKey = TableEditableExample.dataKey(rowIndex, columnIndex);
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
        const dataKey = TableEditableExample.dataKey(rowIndex, columnIndex);
        return (value: string) => {
            const intent = this.isValidValue(value, columnIndex) ? null : Intent.DANGER;
            this.setSparseState("sparseCellIntent", dataKey, intent);
            this.setSparseState("sparseCellData", dataKey, value);
        };
    };

    private cellSetter = (rowIndex: number, columnIndex: number) => {
        const dataKey = TableEditableExample.dataKey(rowIndex, columnIndex);
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


}
