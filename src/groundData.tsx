import React, { useEffect, useState } from 'react';
import { Cell, Column, ColumnHeaderCell, EditableCell, EditableName, Table } from "@blueprintjs/table";
import { Intent } from '@blueprintjs/core';

interface ITableEditableExampleState {
    columnNames: string[];
    sparseCellData: { [key: string]: string };
    sparseCellIntent: { [key: string]: Intent };
    sparseColumnIntents: Intent[];
}

function GroundData() {

    const state: ITableEditableExampleState = {
        columnNames: ["Please", "Rename", "Me"],
        sparseCellData: {
            "1-1": "editable",
            "3-1": "validation 123",
        },
        sparseCellIntent: {
            "3-1": Intent.DANGER,
        },
        sparseColumnIntents: [],
    };

    const [exampleTable, setExampleTable] = useState<ITableEditableExampleState>(state);

    const dataKey = (rowIndex: number, columnIndex: number) => {
        return `${rowIndex}-${columnIndex}`;
    };

    const columns = exampleTable.columnNames.map((_: string, index: number) => {
        return (
            <Column key={index} cellRenderer={renderCell} columnHeaderCellRenderer={renderColumnHeader} />
        );
    })

    const renderCell = (rowIndex: number, columnIndex: number) => {
        const key = dataKey(rowIndex, columnIndex);
        const value = exampleTable.sparseCellData[key];
        return (
            <EditableCell
                value={value == null ? "" : value}
                intent={exampleTable.sparseCellIntent[key]}
                // onCancel={cellValidator(rowIndex, columnIndex)}
                // onChange={cellValidator(rowIndex, columnIndex)}
                // onConfirm={cellSetter(rowIndex, columnIndex)}
            />
        );
    };

    const renderColumnHeader = (columnIndex: number) => {
        const nameRenderer = (name: string) => {
            return (
                <EditableName
                    name={name}
                    intent={exampleTable.sparseColumnIntents[columnIndex]}
                    // onChange={this.nameValidator(columnIndex)}
                    // onCancel={this.nameValidator(columnIndex)}
                    // onConfirm={this.nameSetter(columnIndex)}
                />
            );
        };
        return <ColumnHeaderCell name={exampleTable.columnNames[columnIndex]} nameRenderer={nameRenderer} />;
    };

    return (
        <div>
            <Table numRows={7}>{columns}</Table>
        </div>
    );
}

export default GroundData;
