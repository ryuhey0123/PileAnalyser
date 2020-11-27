import React, { useContext } from 'react';
import { CartesianGrid, Line, LineChart, Tooltip, XAxis, YAxis } from 'recharts';

import EditableTableContext from '../editableTableContext';


const SoilTableGraph = (props: { columnIndex: number, rowSize: number }) => {

  const { state } = useContext(EditableTableContext)

  const chartData = (columnIndex: number, rowSize: number) => {
    const depthIndex = 0;
    const result = [...Array(rowSize)].map((_, i) => {
      if (state.tableData.sparseCellData) {
        return {
          x: parseFloat(state.tableData.sparseCellData[`${i}-${depthIndex}`]),
          y: parseFloat(state.tableData.sparseCellData[`${i}-${columnIndex}`])
        };
      } else {
        return { x: 0, y: 0 }
      };
    });
    return result
  };

  const AreaChartBy = () => (
    <LineChart layout="vertical" data={chartData(props.columnIndex, props.rowSize)}
      width={300} height={670} margin={{top: 0, right: 30, left: 0, bottom: 0}} >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis type="number" orientation="top" domain={[0, 60]} />
      <YAxis dataKey="x" />
      <Tooltip />
      <Line type='linear' dataKey="y"/>
    </LineChart>
  )

  return (
    <div>
      <AreaChartBy />
    </div>
  );
};

export default SoilTableGraph;
