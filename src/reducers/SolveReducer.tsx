// actionをstateに変換
export interface IInputs {
    [key: string]: number | string
}

export interface IOutput {
    [key: string]: number
}

export interface IState {
    inputs: IInputs,
    outputs: IOutput[]
}

export const initialState: IState = {
    inputs: {
        condition: 1.0,
        diameter: 1300,
        length: 17.5,
        level: -2.5,
        force: 500,
        div_num: 100,
        mode: 'non_liner',
        bottom_condition: 'pin',
        material: 'concrete',
    },
    outputs: [
        {x: 0, dec: 0, kh0s: 0, y: 0, t: 0, m: 0, q: 0},
    ],
}

export function AppReducer(preState: IState, action: IOutput[]) {
    const state: IState = {
        inputs: preState.inputs,
        outputs: action
    }
    return state
}
