# MUI React Hook Form Field Adapter Reference

## Purpose

Illustrate a typed controlled `TextField` adapter for compatible Material UI
and React Hook Form versions.

## Applies when

Apply when the `mui-react-hook-form` preset is selected and the installed
`TextField` exposes the illustrated controlled API.

## Does not apply when

Do not copy ref, slot or event semantics to another MUI component without
checking its installed-version contract.

## Reference

```tsx
import TextField, { type TextFieldProps } from "@mui/material/TextField";
import { useId } from "react";
import {
  Controller,
  type FieldValues,
  type Path,
  useFormContext,
} from "react-hook-form";

type FormTextFieldProps<Values extends FieldValues> = Omit<
  TextFieldProps,
  | "defaultValue"
  | "error"
  | "inputRef"
  | "name"
  | "onBlur"
  | "onChange"
  | "value"
> & {
  name: Path<Values>;
};

export function FormTextField<Values extends FieldValues>(
  props: FormTextFieldProps<Values>,
) {
  const generatedId = useId();
  const { helperText, id = generatedId, name, ...rest } = props;
  const { control } = useFormContext<Values>();

  return (
    <Controller
      control={control}
      name={name}
      render={({ field, fieldState }) => (
        <TextField
          {...rest}
          id={id}
          name={field.name}
          value={field.value ?? ""}
          onBlur={field.onBlur}
          onChange={field.onChange}
          inputRef={field.ref}
          error={fieldState.invalid}
          helperText={fieldState.error?.message ?? helperText}
        />
      )}
    />
  );
}
```

## Adaptation notes

- Follow the [MUI React Hook Form Fields
  rule](../../rules/stacks/mui/react-hook-form-fields.md).
- Map the focus ref through the target component's real input or slot contract.
- Define separate conversions for numbers, booleans, Autocomplete values and
  multiple selections; the empty-string mapping above is text-field specific.
- Keep schemas, labels and product validation in the consuming slice.

## Checklist

- [ ] The installed `TextField` API matches the controlled props and `inputRef`.
- [ ] The field name is typed against the owning form values.
- [ ] Form-owned props cannot be replaced through rest props.
- [ ] Validation feedback and label association remain accessible.
