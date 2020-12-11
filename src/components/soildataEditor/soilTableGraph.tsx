import React, { useContext } from 'react';
import { CartesianGrid, Line, LineChart, ReferenceArea, ReferenceLine, Tooltip, XAxis, YAxis } from 'recharts';

import EditableTableContext from '../../editableTableContext';


const SoilTableGraph = (props: { columnIndex: number, rowSize: number }) => {

  const pilePosition = 45;
  const depthIndex = 0;

  const pileLevelFromGL = 1.5;
  const pileLength = 17.0;
  const borLevelFromKBM = -0.4;
  const groundLevelFromKBM = -0.3;

  const { state } = useContext(EditableTableContext)

  const chartData = (columnIndex: number, rowSize: number) => {
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

  const groundLevelFromBor = borLevelFromKBM - groundLevelFromKBM;
  const pileTopLevelFromBor = pileLevelFromGL - groundLevelFromBor;
  const pileBottomLevelFromBor = pileTopLevelFromBor + pileLength;

  const AreaChartBy = () => (
      <LineChart layout="vertical" data={chartData(props.columnIndex, props.rowSize)}
        width={250} height={670} margin={{ top: 0, right: 30, bottom: 0, left: -25 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis type="number" orientation="top" domain={[0, 60]} />
        <YAxis dataKey="x" />
        <Tooltip />
        <Line type='linear' dataKey="y"/>
        <ReferenceArea stroke="red" strokeOpacity={0.3}
          x1={pilePosition - 5} x2={pilePosition + 5}
          y1={pileTopLevelFromBor} y2={pileBottomLevelFromBor} />
        <ReferenceLine y={pileTopLevelFromBor} stroke="red" strokeDasharray="3 3"
          label={`BOR-${pileTopLevelFromBor}m`} />
        <ReferenceLine y={pileBottomLevelFromBor} stroke="red" strokeDasharray="3 3"
          label={`BOR-${pileBottomLevelFromBor}m`} />
      </LineChart>
  )

  return (
    <div>
      <AreaChartBy />
    </div>
  );
};

export default SoilTableGraph;
