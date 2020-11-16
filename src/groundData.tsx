import React, { useEffect, useState } from 'react';
import { Column, EditableCell, Table } from "@blueprintjs/table";

interface SoilData {
    [key: string]: any[]
};

function GroundData() {


    const columns: string[] = ["depth", "nValue", "soil", "reductions", "adopted_reductions", "alpha", "E0"];
    const columnsJPN: string[] = ["深度", "N値", "土質", "低減係数", "採用低減係数", "α", "E0"];

    const [data, setData] = useState<SoilData>({});
    const [hook] = useState();

    useEffect(() => {
        fetch("/upload", {
            method: "POST",
        })
        .then(res => res.json())
        .then(data => setData(data))
    }, [hook]);

    const renderCell = (rowIndex: number, columnIndex: number) => {
        const column: string = columns[columnIndex];
        const value = data[column] ? data[column][rowIndex] : "";
        return (
            <EditableCell
                value={value}
                // intent={this.state.sparseCellIntent[dataKey]}
                // onCancel={this.cellValidator(rowIndex, columnIndex)}
                // onChange={this.cellValidator(rowIndex, columnIndex)}
                onConfirm={onConfirmHandle(rowIndex, columnIndex)}
            />
        );
    };

    const cellValudator = (rowIndex: number, columnIndex: number) => {
        return (value: string) => {

        };
    };

    const onConfirmHandle = (rowIndex: number, columnIndex: number) => {
        return (value: string) => {
            const column: string = columns[columnIndex];
            setData( () => {
                data[column].splice(rowIndex, 1, value)
                return data
            })
        };
    };

    const numRows = data[columns[0]]?.length;
    const renderColumn = columns.map((_: string, index: number) =>
        <Column name={columnsJPN[index]} key={index} cellRenderer={renderCell} />
    );

    return (
        <div>
            <Table numRows={numRows}>{renderColumn}</Table>
        </div>
    );
}

export default GroundData;
