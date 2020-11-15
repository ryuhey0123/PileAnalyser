import React, { useEffect, useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer} from 'recharts';

function Chart() {
    const [data, setData] = useState([{}]);

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

    const AreaChartBy = (dataKey: string, unit: string, stroke='#8884b8', fill='#8884d8') => (
        <ResponsiveContainer width='80%' height={200}>
            <AreaChart data={data} syncId="anyId">
                <CartesianGrid strokeDasharray="3 3"/>
                <XAxis dataKey="x"/>
                <YAxis/>
                <Tooltip/>
                <Area type='linear' unit={unit} dataKey={dataKey} stroke={stroke} fill={fill} />
            </AreaChart>
        </ResponsiveContainer>
    )

    return (
        <div>
            {AreaChartBy("kh0s", "kN/m3")}
            {AreaChartBy("dec", "")}
            {AreaChartBy("y", "mm")}
            {AreaChartBy("t", "rad")}
            {AreaChartBy("m", "kNm")}
            {AreaChartBy("q", "kN")}
        </div>
    );
};

export default Chart;
