import React, { useEffect, useState } from 'react';
import { Cell, Column, Table } from "@blueprintjs/table";


interface SoilData {
    depth: number[],
    nValue: number[],
    soil: string[],
    reductions: number[],
    adopted_reductions: number[],
    alpha: number[],
    E0: number[],
};

function GroundData() {
    const initSoilData: SoilData = {
        depth: [],
        nValue: [],
        soil: [],
        reductions: [],
        adopted_reductions: [],
        alpha: [],
        E0: []
    }
    const [data, setData] = useState<SoilData>(initSoilData);

    useEffect(() => {
        fetch("/upload", {
            method: "POST",
        })
            .then(res => res.json())
            .then(data => setData(data))
    }, []);

    const cellRenderer = (columnData: Array<number | string>) => {
        return (rowIndex: number) => {
            return <Cell>{columnData[rowIndex]}</Cell>
        }
    }

    return (
        <div>
            <Table numRows={data.depth.length}>
                <Column name="深度" cellRenderer={cellRenderer(data.depth)}/>
                <Column name="N値" cellRenderer={cellRenderer(data.nValue)}/>
                <Column name="土質" cellRenderer={cellRenderer(data.soil)}/>
                <Column name="低減係数" cellRenderer={cellRenderer(data.reductions)}/>
                <Column name="採用低減係数" cellRenderer={cellRenderer(data.adopted_reductions)}/>
                <Column name="α" cellRenderer={cellRenderer(data.alpha)}/>
                <Column name="E0" cellRenderer={cellRenderer(data.E0)}/>
            </Table>
        </div>
    );
}

export default GroundData;
