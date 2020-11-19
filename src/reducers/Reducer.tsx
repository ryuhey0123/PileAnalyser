// actionをstateに変換
// イコールDispatch

export interface IInputs {
    [key: string]: number | string
}

export interface IOutputs {
    results: {[key: string]: number}[]
    time: string
}

export interface IState {
    inputs: IInputs,
    outputs: IOutputs
}

export interface IAction {
    type: "input" | "output",
    results: IState
}

export const initialState: IState = {
    inputs: {
        mode: "non_liner_multi",
        bottom_condition: "pin",
        material: "concrete",
        condition: 1.0,
        diameter: 1300,
        length: 17.5,
        level: -2.5,
        force: 500,
    },
    outputs: {
        results: [{}],
        time: ""
    },
}

export function Reducer(preState: IState, action: IAction) {
    switch (action.type) {

        case "output":
            const newOutState: IState = {
                inputs: preState.inputs,
                outputs: action.results.outputs
            }
            return newOutState

        case "input":
            const newInState: IState = {
                inputs: preState.inputs,
                outputs: preState.outputs
            }
            for (const key in action.results.inputs) {
                newInState.inputs[key] = action.results.inputs[key];
            };
            console.log(newInState)
            return newInState
    }
}
