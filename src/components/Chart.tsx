import React, { useContext } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer} from 'recharts';
import Context from '../Context';

const Chart = () => {

    const { state } = useContext(Context)

    const AreaChartBy = (dataKey: string, unit: string, stroke='#8884b8', fill='#8884d8') => (
        <ResponsiveContainer height={150}>
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
            {/* <label>水平地盤反力係数(低減前)</label>
            {AreaChartBy("kh0s", "kN/m3")} */}
            <label>地地盤変位による低減係数</label>
            {AreaChartBy("dec", "", '#ED9D39', '#ED9D39')}
            <label>変位</label>
            {AreaChartBy("y", "mm", '#225098', '#225098')}
            {/* <p>変形角</p> */}
            {/* {AreaChartBy("t", "rad")} */}
            <label>曲げモーメント</label>
            {AreaChartBy("m", "kNm", '#D32E44', '#D32E44')}
            <label>剪断力</label>
            {AreaChartBy("q", "kN", '#408A55', '#408A55')}
        </div>
    );
};

export default Chart;
