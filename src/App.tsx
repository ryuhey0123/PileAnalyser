import React, {useState} from 'react';

import { Button, FormControl, FormControlLabel, FormLabel, Grid, Input, Slider } from '@material-ui/core';
import { Radio, RadioGroup } from '@material-ui/core';
import { Typography } from '@material-ui/core';
// import './App.css';


function App() {
  const [modeValue, setModeValue] = useState('non_liner_multi');
  const [bottomConditionValue, setBottomConditionValue] = useState('pin');
  const [materialValue, setMaterialValue] = useState('concrete');

  const [conditionValue, setConditionValue] = useState<number | string | Array<number | string>>(1.00);

  const handleSliderChange = (event: any, newValue: number | number[]) => {
    setConditionValue(newValue);
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setConditionValue(event.target.value === '' ? '' : Number(event.target.value));
  };

  return (
    <div className="{classes.root">
      <header className="App-header">
        <Typography variant="h2">多層地盤中の杭の非線形解析</Typography>
        <Typography variant="body1">弾性支承梁の微分方程式を差分法によって解析し、杭の応力を算出する。</Typography>

        <FormControl component="fieldset">

          <FormLabel component="legend">解析モード</FormLabel>
          <RadioGroup name="mode" value={modeValue} onChange={(e) => {setModeValue(e.target.value)}}>
            <FormControlLabel value="non_liner_multi" control={<Radio />} label="非線形(多層地盤)" />
            <FormControlLabel value="non_liner_single" control={<Radio />} label="非線形(単層地盤)" />
            <FormControlLabel value="liner" control={<Radio />} label="線形" />
          </RadioGroup>

          <FormLabel component="legend">杭脚条件</FormLabel>
          <RadioGroup name="bottom_condition" value={bottomConditionValue} onChange={(e) => {setBottomConditionValue(e.target.value)}}>
            <FormControlLabel value="pin" control={<Radio />} label="ピン" />
            <FormControlLabel value="free" control={<Radio />} label="自由" />
          </RadioGroup>

          <FormLabel component="legend">材質</FormLabel>
          <RadioGroup name="material" value={materialValue} onChange={(e) => {setMaterialValue(e.target.value)}}>
            <FormControlLabel value="concrete" control={<Radio />} label="コンクリート" />
            <FormControlLabel value="steel" control={<Radio />} label="鋼材" />
          </RadioGroup>

          <Typography gutterBottom>杭頭固定度</Typography>
          <Slider
            step={0.001}
            min={0.000}
            max={1.000}
            value={typeof conditionValue === 'number' ? conditionValue : 1}
            onChange={handleSliderChange}
          />
          <Input
            value={conditionValue}
            onChange={handleInputChange}
            inputProps={{
              step: 0.001,
              min: 0,
              max: 1.0,
              type: 'number',
              'aria-labelledby': 'input-slider'
              }}
          />

          <FormLabel component="legend">杭径(m)</FormLabel>
          <Input type="number" name="diameter" value="1300"></Input>

          <FormLabel component="legend">杭長(m)</FormLabel>
          <Input type="number" name="pile_length" value="1300"></Input>

          <FormLabel component="legend">杭天端(m)</FormLabel>
          <Input type="number" name="level" value="1300"></Input>

          <FormLabel component="legend">入力水平力(kN)</FormLabel>
          <Input type="number" name="force" value="1300"></Input>

          <Button type="button">Solve</Button>

        </FormControl>

      </header>
    </div>
  );
}

export default App;
