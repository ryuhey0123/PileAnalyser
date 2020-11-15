import React, { useEffect, useState } from 'react';
import {LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip} from 'recharts';

function Chart() {
    const [data, setData] = useState([
        {x: 0, dec: 0, kh0s: 0, y: 0, t: 0, m: 0, q: 0}
    ]);

    const [inputData] = useState({
        mode: 'non_liner',
        condition: 1.0,
        bottom_condition: 'pin',
        material: 'concrete',
        diameter: 1300,
        length: 17.5,
        level: -2.0,
        force: 1000,
        div_num: 100
    });

    useEffect(() => {
        fetch("/solve", {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(inputData)
        })
        .then(res => res.json())
        .then(data => setData(data.results))
    }, [inputData]);

    const AreaChartBy= (dataKey: string, stroke='#8884b8', fill='#8884d8') => (
        <AreaChart width={600} height={200} data={data} syncId="anyId" margin={{top: 10, right: 30, left: 0, bottom: 0}}>
            <CartesianGrid strokeDasharray="3 3"/>
            <XAxis dataKey="x"/>
            <YAxis/>
            <Tooltip/>
            <Area type='monotone' dataKey={dataKey} stroke={stroke} fill={fill} />
        </AreaChart>
    )

    return (
        <div>
            {AreaChartBy("dec")}
            {AreaChartBy("kh0s")}
            {AreaChartBy("y")}
            {AreaChartBy("t")}
            {AreaChartBy("m")}
            {AreaChartBy("q")}
        </div>
    );
};

export default Chart;
