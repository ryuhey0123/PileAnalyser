import React, { useContext } from 'react';
import { CartesianGrid, Line, LineChart, XAxis, YAxis } from 'recharts';

import EditableTableContext from '../editableTableContext';


const SoilTableGraph = () => {

  const { state } = useContext(EditableTableContext)

  const AreaChartBy = () => (
    <LineChart layout="vertical" width={300} height={670} data={state.graphData.nValues}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis orientation="top"/>
      <YAxis dataKey="x"/>
      <Line type='linear' dataKey="kh0s"/>
    </LineChart>
  )

  return (
    <div>
      <AreaChartBy/>
    </div>
  );
};

export default SoilTableGraph;
