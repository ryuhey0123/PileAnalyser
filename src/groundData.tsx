import React, { useEffect, useState } from 'react';
import { Cell, Column, Table } from "@blueprintjs/table";


function GroundData() {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch("/upload").then(res => res.json()).then(data => {
            console.log(data.depth)
        });
    }, []);

    const cellRenderer = (rowIndex: number) => {
        return <Cell>{`$${(rowIndex * 10).toFixed(2)}`}</Cell>
    };

    return (
        <div>
            {data}
            <Table numRows={15}>
                <Column name="Dollars" cellRenderer={cellRenderer}/>
            </Table>
        </div>
    );
}

export default GroundData;
