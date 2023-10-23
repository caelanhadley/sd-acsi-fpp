module portTest {
    queued component MathReceiver {

    # ----------------------------------------------------------------------
    # General ports
    # ----------------------------------------------------------------------

    @ Port for receiving the math operation
    async input port mathOpIn: OpRequest

    @ Port for returning the math result
    output port mathResultOut: MathResult

    @ The rate group scheduler input
    sync input port schedIn: Svc.Sched

    }
}