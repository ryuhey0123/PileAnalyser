import React, { useContext } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer} from 'recharts';
import Context from '../Context';

const Chart = () => {

    const { state } = useContext(Context)

    const AreaChartBy = (dataKey: string, unit: string, stroke='#8884b8', fill='#8884d8') => (
        <ResponsiveContainer width='80%' height={200}>
            <AreaChart data={state.outputs.results} syncId="anyId">
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
