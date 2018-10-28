// Imports

// Actions
const START_TIMER = 'START_TIMER';
const PAUSE_TIMER = 'PAUSE_TIMER';
const RESUME_TIMER = 'RESUME_TIMER';
const STOP_TIMER = 'STOP_TIMER';
const ADD_SECOND = 'ADD_SECOND';

// Action Creators
function startTimer() {
    return {
        type: START_TIMER,
    };
}

function pauseTimer() {
    return {
        type: PAUSE_TIMER,
    };
}

function resumeTimer() {
    return {
        type: RESUME_TIMER,
    };
}

function stopTimer() {
    return {
        type: STOP_TIMER,
    };
}

function addSecond() {
    return {
        type: ADD_SECOND,
    };
}

// Reducer Functions
const TIMER_DURATION = 1500;

function applyStatTimer(state) {
    return {
        ...state,
        isPlaying: true,
        elapsedTime: 0,
    };
}

function applyPauseTimer(state) {
    return {
        ...state,
        isPlaying: false,
    };
}


function applyResumeTimer(state) {
    return {
        ...state,
        isPlaying: true,
    };
}

function applyStopTimer(state) {
    return {
        ...state,
        isPlaying: false,
        elapsedTime: 0,
    };
}

function applyAddSecond(state) {
    const { elapsedTime } = state;
    if (elapsedTime < TIMER_DURATION) {
        return {
            ...state,
            elapsedTime: elapsedTime + 1,
        };
    }
    return {
        ...state,
        isPlaying: false,
    };
}

// Reducer

const initialState = {
    isPlaying: false,
    elapsedTime: 0,
    timerDuration: TIMER_DURATION,
};

function reducer(state = initialState, action) {
    switch (action.type) {
    case START_TIMER:
        return applyStatTimer(state);
    case PAUSE_TIMER:
        return applyPauseTimer(state);
    case RESUME_TIMER:
        return applyResumeTimer(state);
    case STOP_TIMER:
        return applyStopTimer(state);
    case ADD_SECOND:
        return applyAddSecond(state);
    default:
        return state;
    }
}

// Exports
const actionCreators = {
    startTimer,
    stopTimer,
    pauseTimer,
    resumeTimer,
    addSecond,
};

export { actionCreators };

// Default
export default reducer;
