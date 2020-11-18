// actionをstateに変換
export interface IInputs {
    [key: string]: number | string
}

export interface IResult {
    [key: string]: number
}

export interface IState {
    inputs: IInputs,
    outputs: {
        results: IResult[]
        time: string
    }
}

export const initialState: IState = {
    inputs: {},
    outputs: {
        results: [{}],
        time: ""
    },
}

export function AppReducer(preState: IState, action: {[key: string]: number}[]) {
    const state: IState = {
        inputs: preState.inputs,
        outputs: {
            results: action,
            time: ""
        }
    }
    return state
}
