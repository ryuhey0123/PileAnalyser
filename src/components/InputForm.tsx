import React, { useContext } from 'react';
import { Button, Label, NumericInput, Radio, RadioGroup } from '@blueprintjs/core';
import { inputValueChange, solve } from '../actions/actionCreator';
import Context from '../context';
import { initialState } from '../reducers/reducer';

const InputForm = () => {

  const { state, dispatch } = useContext(Context)

  const onValueChange = (valueAsNumber: number, _: string, inputElement: HTMLInputElement | null) => {
    if (inputElement != null) {
      dispatch(inputValueChange(inputElement.id, valueAsNumber));
    };
  };

  return (
    <div>
      <RadioGroup
        label="解析モード"
        onChange={e => dispatch(inputValueChange("mode", e.currentTarget.value))}
        selectedValue={state.inputs.mode}
      >
        <Radio label="非線形(多層地盤)" value="non_liner_multi" />
        <Radio label="非線形(単層地盤)" value="non_liner_single" />
        <Radio label="線形" value="liner" />
      </RadioGroup>
      <RadioGroup
        label="杭脚条件"
        onChange={e => dispatch(inputValueChange("bottom_condition", e.currentTarget.value))}
        selectedValue={state.inputs.bottom_condition}
      >
        <Radio label="ピン" value="pin" />
        <Radio label="自由" value="free" />
      </RadioGroup>
      <RadioGroup
        label="材質"
        onChange={e => dispatch(inputValueChange("material", e.currentTarget.value))}
        selectedValue={state.inputs.material}>
        <Radio label="コンクリート" value="concrete" />
        <Radio label="鋼材" value="steel" />
      </RadioGroup>

      <Label>杭頭固定度
        <NumericInput id="condition" defaultValue={initialState.inputs.condition}
          max={1.0} min={0.0} stepSize={0.001} minorStepSize={0.001} majorStepSize={0.1} onValueChange={onValueChange} />
      </Label>
      <Label>杭径(mm)
        <NumericInput id="diameter" defaultValue={initialState.inputs.diameter}
          min={0.0} stepSize={10} minorStepSize={10} majorStepSize={100} onValueChange={onValueChange} />
      </Label>
      <Label>杭長(m)
        <NumericInput id="length" defaultValue={initialState.inputs.length}
          min={0.0} stepSize={0.1} minorStepSize={0.1} majorStepSize={1} onValueChange={onValueChange} />
      </Label>
      <Label>杭天端(m)
        <NumericInput id="level" defaultValue={initialState.inputs.level}
          stepSize={0.1} minorStepSize={0.1} majorStepSize={1} onValueChange={onValueChange} />
      </Label>
      <Label>入力水平力(kN)
        <NumericInput id="force" defaultValue={initialState.inputs.force}
          min={0.0} stepSize={10} minorStepSize={10} majorStepSize={100} onValueChange={onValueChange} />
      </Label>

      <Button intent="none" icon="grid" text="Soil data"
        onClick={()=>{}} />

      <Button intent="primary" icon="tick" text="Solve"
        onClick={() => solve(state, dispatch)} />

    </div>
  );
}

export default InputForm;
