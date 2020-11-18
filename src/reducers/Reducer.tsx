export function AppReducer(state, action) {
    var NewonState = state.onState.slice();

    switch(action.type){
        case 'toggle':
            var i = action.data.button;
            NewisPlayed[i] = !state.onState[i];
            return {onState: NewonState}
        case 'reset':
            var filledfalse = Array(10).fill(false);
            return {onState: filledfalse}
        default:
            return state;
    }
}
