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
            <p>水平地盤反力係数(低減前)</p>
            {AreaChartBy("kh0s", "kN/m3")}
            <p>地地盤変位による低減係数</p>
            {AreaChartBy("dec", "")}
            <p>変位</p>
            {AreaChartBy("y", "mm")}
            <p>変形角</p>
            {AreaChartBy("t", "rad")}
            <p>曲げモーメント</p>
            {AreaChartBy("m", "kNm")}
            <p>剪断力</p>
            {AreaChartBy("q", "kN")}
        </div>
    );
};

export default Chart;
