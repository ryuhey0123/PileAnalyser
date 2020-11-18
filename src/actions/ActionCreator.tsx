// dispatchにactionを入れ込む
// そのactionはreducerでstateに変換される

import { IResults } from "../reducers/SolveReducer";

export async function solve(inputValues: any, modeValue: string, btmConditionValue: string, materialValue: string, dispatch: ((arg0: IResults) => void)) {

    inputValues["mode"] = modeValue;
    inputValues["bottom_condition"] = btmConditionValue;
    inputValues["material"] = materialValue;
    inputValues["div_num"] = 100;

    fetch("/solve", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(inputValues)
    })
    .then((res) => res.json())
    .then((action) => {
        dispatch(action);
    })
}
