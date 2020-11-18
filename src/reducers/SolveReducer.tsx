// actionをstateに変換
export interface IInputs {
    [key: string]: number | string
}

export interface IResults {
    results: {[key: string]: number}[]
    time: string
}

export interface IState {
    inputs: IInputs,
    outputs: IResults
}

export const initialState: IState = {
    inputs: {},
    outputs: {
        results: [{}],
        time: ""
    },
}

export function AppReducer(preState: IState, action: IResults) {
    const state: IState = {
        inputs: preState.inputs,
        outputs: action
    }
    return state
}
