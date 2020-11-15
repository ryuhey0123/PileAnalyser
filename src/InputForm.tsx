import React, { useState } from 'react';
import { Button, Label, NumericInput, Radio, RadioGroup } from '@blueprintjs/core';

import Chart from './Chart';

function InputForm() {
    interface Inputs {
        [key: string]: any
    };

    const [inputValues, setInputValues] = useState<Inputs>({
        condition: 1.0,
        diameter: 1300,
        length: 17.5,
        level: -2.5,
        force: 500,
    });
    const [outputValues, setOutputValues] = useState();

    const [modeValue, setModeValue] = useState("non_liner_multi");
    const [btmConditionValue, setBtmConditionValue] = useState("pin");
    const [materialValue, setMaterialValue] = useState("concrete");

    const appendValue = (key: string, value: any) => {
        inputValues[key] = value;
        return inputValues
    };

    const onValueChange = (valueAsNumber: number, valueAsString: string, inputElement: HTMLInputElement | null) => {
        if (inputElement != null) {
            setInputValues(appendValue(inputElement.id, valueAsNumber))
        };
    };

    const onClick = (e: React.MouseEvent<HTMLElement>) => {
        inputValues["mode"] = modeValue;
        inputValues["bottom_condition"] = btmConditionValue;
        inputValues["material"] = materialValue;
        inputValues["div_num"] = 100;

        fetch("/solve", {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(inputValues)
        })
        .then(res => res.json())
        .then(data => setOutputValues(data.results))

        console.log(inputValues);
        console.log(outputValues);
    }

    return (
        <div>
            <RadioGroup label="解析モード" onChange={e => setModeValue(e.currentTarget.value)} selectedValue={modeValue}>
                <Radio label="非線形(多層地盤)" value="non_liner_multi" />
                <Radio label="非線形(単層地盤)" value="non_liner_single" />
                <Radio label="線形" value="liner" />
            </RadioGroup>
            <RadioGroup label="杭脚条件" onChange={e => setBtmConditionValue(e.currentTarget.value)} selectedValue={btmConditionValue}>
                <Radio label="ピン" value="pin" />
                <Radio label="自由" value="free" />
            </RadioGroup>
            <RadioGroup label="材質" onChange={e => setMaterialValue(e.currentTarget.value)} selectedValue={materialValue}>
                <Radio label="コンクリート" value="concrete" />
                <Radio label="鋼材" value="steel" />
            </RadioGroup>

            <Label>杭頭固定度
                <NumericInput id="condition" defaultValue={inputValues["condition"]}
                    max={1.0} min={0.0} stepSize={0.001} minorStepSize={0.001} majorStepSize={0.1} onValueChange={onValueChange} />
            </Label>
            <Label>杭径(mm)
                <NumericInput id="diameter" defaultValue={inputValues["diameter"]}
                    min={0.0} stepSize={10} minorStepSize={10} majorStepSize={100} onValueChange={onValueChange} />
            </Label>
            <Label>杭長(m)
                <NumericInput id="length" defaultValue={inputValues["length"]}
                    min={0.0} stepSize={0.1} minorStepSize={0.1} majorStepSize={1} onValueChange={onValueChange} />
            </Label>
            <Label>杭天端(m)
                <NumericInput id="level" defaultValue={inputValues["level"]}
                    stepSize={0.1} minorStepSize={0.1} majorStepSize={1} onValueChange={onValueChange} />
            </Label>
            <Label>入力水平力(kN)
                <NumericInput id="force" defaultValue={inputValues["force"]}
                    min={0.0} stepSize={10} minorStepSize={10} majorStepSize={100} onValueChange={onValueChange} />
            </Label>

            <Button intent="primary" icon="tick" text="Solve" onClick={onClick} />

            <Chart output={outputValues}/>
        </div>
    );
}

export default InputForm;
