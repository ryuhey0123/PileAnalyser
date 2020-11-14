import React, { useEffect, useState } from 'react';
import { Cell, Column, Table } from "@blueprintjs/table";

type SoilData = {
    depth: number[];
    nValue: number[];
    soil: string[];
    reductions: number[];
    adopted_reductions: number[];
    alpha: number[];
    E0: number[];
};

function GroundData() {
    const [data, setData] = useState<SoilData | undefined>(undefined);

    useEffect(() => {
        fetch("/upload", {
            method: "POST",
        })
            .then(res => res.json())
            .then(data => setData(data))
    }, []);

    const cellRenderer = (rowIndex: number) => {
        return <Cell>{`$${(rowIndex * 10).toFixed(2)}`}</Cell>
    };

    return (
        <div>
            { data?.depth }
            <Table numRows={15}>
                <Column name="Dollars" cellRenderer={cellRenderer}/>
            </Table>
        </div>
    );
}

export default GroundData;
