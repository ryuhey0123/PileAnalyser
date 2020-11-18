import { createContext } from "react";

export const AppContext = createContext({
    state: {
        onState: Array(10).fill(false)
    },
    dispatch: null
})
