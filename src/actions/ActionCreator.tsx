export function solveButton(dispatch, button) {
    const action = {
        type: "solve",
        data: {
            button: button
        }
    }
    dispatch(action);
}
