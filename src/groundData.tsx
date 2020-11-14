import React, { useEffect, useState } from 'react';
import { Column, EditableCell, Table } from "@blueprintjs/table";


function GroundData() {
    interface SoilData {
        [key: string]: any[]
    };

    const columns: string[] = ["depth", "nValue", "soil", "reductions", "adopted_reductions", "alpha", "E0"];
    const columnsJPN: string[] = ["深度", "N値", "土質", "低減係数", "採用低減係数", "α", "E0"];

    const [data, setData] = useState<SoilData>({});

    useEffect(() => {
        fetch("/upload", {
            method: "POST",
        })
        .then(res => res.json())
        .then(data => setData(data))
    });

    const renderCell = (rowIndex: number, columnIndex: number) => {
        const column: string = columns[columnIndex];
        const value = data[column] ? data[column][rowIndex] : "";
        return (
            <EditableCell
                value={value}
                // intent={this.state.sparseCellIntent[dataKey]}
                // onCancel={this.cellValidator(rowIndex, columnIndex)}
                // onChange={this.cellValidator(rowIndex, columnIndex)}
                // onConfirm={this.cellSetter(rowIndex, columnIndex)}
            />
        );
    };

    const renderColumn = columns.map((_: string, index: number) =>
        <Column name={columnsJPN[index]} key={index} cellRenderer={renderCell} />
    );

    const numRows = data[columns[0]]?.length;

    return (
        <div>
            <Table numRows={numRows}>{renderColumn}</Table>
        </div>
    );
}

export default GroundData;
