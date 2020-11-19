// dispatchにactionを入れ込む
// そのactionはreducerでstateに変換される

import { IAction, IState } from "../reducers/Reducer";

export async function solve(state: IState, dispatch: ((arg: IAction) => void)) {

    fetch("/solve", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(state.inputs)
    })
    .then((res) => res.json())
    .then((data) => {
        const action: IAction = {
            type: "output",
            outputs: data
        }
        dispatch(action);
    })
}

export function inputValueChange(key: string, value: number | string, dispatch: ((arg: IAction) => void)) {
    const action: IAction = {
        type: "input",
        inputs: {[key]: value},
    }
    dispatch(action)
}
