import React, { useState } from 'react';
import { Button, Label, NumericInput, Radio, RadioGroup } from '@blueprintjs/core';


function InputForm() {
  const [modeValue, setModeValue] = useState('non_liner_multi');
  const [bottomConditionValue, setBottomConditionValue] = useState('pin');
  const [materialValue, setMaterialValue] = useState('concrete');

  return (
    <div>
      <RadioGroup label="解析モード" onChange={(e) => setModeValue(e.currentTarget.value)} selectedValue={modeValue}>
        <Radio label="非線形(多層地盤)" value="non_liner_multi" />
        <Radio label="非線形(単層地盤)" value="non_liner_single" />
        <Radio label="線形" value="liner" />
      </RadioGroup>
      <RadioGroup label="杭脚条件" onChange={(e) => setBottomConditionValue(e.currentTarget.value)} selectedValue={bottomConditionValue}>
        <Radio label="ピン" value="pin" />
        <Radio label="自由" value="free" />
      </RadioGroup>
      <RadioGroup label="材質" onChange={(e) => setMaterialValue(e.currentTarget.value)} selectedValue={materialValue}>
        <Radio label="コンクリート" value="concrete" />
        <Radio label="鋼材" value="steel" />
      </RadioGroup>

      <Label>杭頭固定度
        <NumericInput max={1.0} min={0.0} stepSize={0.001} minorStepSize={0.001} majorStepSize={0.1} />
      </Label>
      <Label>杭径(mm)
        <NumericInput min={0.0} stepSize={10} minorStepSize={10} majorStepSize={100} />
      </Label>
      <Label>杭長(m)
        <NumericInput min={0.0} stepSize={0.1} minorStepSize={0.1} majorStepSize={1} />
      </Label>
      <Label>杭天端(m)
        <NumericInput stepSize={0.1} minorStepSize={0.1} majorStepSize={1} />
      </Label>
      <Label>入力水平力(kN)
        <NumericInput min={0.0} stepSize={10} minorStepSize={10} majorStepSize={100} />
      </Label>

      <Button intent="primary" icon="tick" text="Solve" />
    </div>
  );
}

export default InputForm;
