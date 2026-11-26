# HeroUI React Hook Form Field Adapter Reference

## Purpose

Illustrate a typed controlled-field adapter for compatible HeroUI and React
Hook Form versions.

## Applies when

Apply when the `heroui-react-hook-form` preset is selected and the installed
HeroUI component exposes the illustrated controlled API.

## Does not apply when

Do not copy slot names or change-handler semantics without checking the
installed HeroUI major version.

## Reference

```tsx
import {
  FieldError,
  Label,
  SearchField as HeroSearchField,
} from "@heroui/react";
import type { ComponentProps } from "react";
import {
  Controller,
  type FieldValues,
  type Path,
  useFormContext,
} from "react-hook-form";

type HeroSearchFieldProps = ComponentProps<typeof HeroSearchField>;

type FormSearchFieldProps<Values extends FieldValues> = Omit<
  HeroSearchFieldProps,
  "children" | "name" | "onBlur" | "onChange" | "value"
> & {
  label?: string;
  name: Path<Values>;
  placeholder?: string;
};

export function FormSearchField<Values extends FieldValues>(
  props: FormSearchFieldProps<Values>,
) {
  const { label, name, placeholder, ...rest } = props;
  const { control } = useFormContext<Values>();

  return (
    <Controller
      control={control}
      name={name}
      render={({ field, fieldState }) => (
        <HeroSearchField
          {...rest}
          isInvalid={fieldState.invalid || rest.isInvalid}
          name={field.name}
          value={field.value ?? ""}
          onBlur={field.onBlur}
          onChange={(value) => field.onChange(value || null)}
        >
          {label && <Label>{label}</Label>}
          <HeroSearchField.Group>
            <HeroSearchField.SearchIcon />
            <HeroSearchField.Input placeholder={placeholder} />
            <HeroSearchField.ClearButton />
          </HeroSearchField.Group>
          {fieldState.error?.message && (
            <FieldError>{fieldState.error.message}</FieldError>
          )}
        </HeroSearchField>
      )}
    />
  );
}
```

## Adaptation notes

- Follow the [HeroUI React Hook Form Fields
  rule](../../rules/stacks/heroui/react-hook-form-fields.md).
- Adapt value conversion to the actual field contract; numeric, date-range and
  boolean controls require different null and falsy handling.
- Keep schemas, labels and product validation in consuming slices.

## Checklist

- [ ] The installed HeroUI API matches the slots and controlled props.
- [ ] The field name is typed against the owning form values.
- [ ] Form-owned props are omitted from the public wrapper contract.
- [ ] Validation feedback is accessible.
