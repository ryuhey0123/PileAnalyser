import React, { useEffect, useState } from 'react';
import { Column, EditableCell, Table } from "@blueprintjs/table";
import { Intent } from '@blueprintjs/core';

interface SoilData {
    [key: string]: any[]
};

interface SparseCellIntent {
    [key: string]: Intent;
}

function GroundData() {

    const columns: string[] = ["depth", "nValue", "soil", "reductions", "adopted_reductions", "alpha", "E0"];
    const columnsJPN: string[] = ["深度", "N値", "土質", "低減係数", "採用低減係数", "α", "E0"];

    const [soilData, setSoilData] = useState<SoilData>({});
    const [sparseCellIntent, setSparseCellIntent] = useState<SparseCellIntent>({});

    useEffect(() => {
        fetch("/upload", {
            method: "POST",
        })
        .then(res => res.json())
        .then(data => setSoilData(data))
    }, []);

    const dataKey = (rowIndex: number, columnIndex: number) => {
        return `${rowIndex}-${columnIndex}`;
    };

    const renderCell = (rowIndex: number, columnIndex: number) => {
        const key = dataKey(rowIndex, columnIndex);
        const column: string = columns[columnIndex];
        const value = soilData[column][rowIndex];
        return (
            <EditableCell
                value={value}
                intent={sparseCellIntent[key]}
                onCancel={cellValidator(rowIndex, columnIndex)}
                onChange={cellValidator(rowIndex, columnIndex)}
                onConfirm={onConfirmHandle(rowIndex, columnIndex)}
            />
        );
    };

    function isValidValue(value: string) {
        return /^[0-9]*$/.test(value);
    }

    const cellValidator = (rowIndex: number, columnIndex: number) => {
        const key = dataKey(rowIndex, columnIndex)
        return (value: string) => {
            const intent = isValidValue(value) ? Intent.NONE : Intent.DANGER;
            setSparseCellIntent( () => {
                sparseCellIntent[key] = intent;
                return sparseCellIntent
            })
        };
    };

    const onConfirmHandle = (rowIndex: number, columnIndex: number) => {
        const key = dataKey(rowIndex, columnIndex)
        return (value: string) => {
            const intent = isValidValue(value) ? Intent.NONE : Intent.DANGER;
            setSparseCellIntent( () => {
                sparseCellIntent[key] = intent;
                return sparseCellIntent
            })
            const column: string = columns[columnIndex];
            setSoilData( () => {
                soilData[column].splice(rowIndex, 1, value)
                return soilData
            })
        };
    };

    const numRows = soilData[columns[0]]?.length;
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
