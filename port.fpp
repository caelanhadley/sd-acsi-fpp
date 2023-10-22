module portTest {
    @ Port for receiving the math operation
    async input port mathOpIn: OpRequest
    @ Port for receiving the math operation
    sync input port mathOpIn2: OpRequest
    @ Port for receiving the math operation
    guarded input port mathOpIn3: OpRequest
}