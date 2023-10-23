# To-Do

## 10/22/2023 - Caelan
1. Need to add classes for events, commands, and telemetry.
2. Parser should be able to handle all of the above classes and ports and should be able to instantiate their respective class objects.
3. A clean implementation for Handling @ comments as descriptions.
4. Some form of basic script validation. For example, not allowing invalid characters or not having required structures such as module {}.
5. Move the input file name out of get_input and pass it as a parameter from main().
6. As objects are created and filled they should preform some form of validation.

### My recommendations for type management
I think a way of splitting the reserved words into categories associated with their root types. For example async should be a property of Ports and Commands. F32, I8, U16, etc should be a somewhat universal property and should be associated with values. Using some form of type enumeration might be a useful option.