# React Hook Form and Zod Reference

## Purpose

Provide a small form lifecycle reference for React Hook Form with optional Zod
validation.

## Applies when

Apply when `react-hook-form`, `zod` and `@hookform/resolvers` are installed
and the project selected the `react-hook-form-zod-reference` preset.

## Does not apply when

Do not use this reference to choose a UI component library, field adapter,
overlay behavior, notification mechanism or mutation transport.

## Reference

```tsx
import { zodResolver } from "@hookform/resolvers/zod";
import { FormProvider, useForm } from "react-hook-form";

import { editItemSchema, type EditItemValues } from "./edit-item-schema";

type EditItemFormProps = {
  initialValues: EditItemValues;
  onSubmit: (values: EditItemValues) => Promise<void>;
};

export function EditItemForm({ initialValues, onSubmit }: EditItemFormProps) {
  const methods = useForm<EditItemValues>({
    defaultValues: initialValues,
    mode: "onChange",
    resolver: zodResolver(editItemSchema),
  });

  const submit = methods.handleSubmit(async (values) => {
    await onSubmit(values);
  });

  return (
    <FormProvider {...methods}>
      <form onSubmit={submit}>
        {/* Render project-owned field adapters here. */}
        <button disabled={!methods.formState.isValid || methods.formState.isSubmitting}>
          Save
        </button>
      </form>
    </FormProvider>
  );
}
```

## Adaptation notes

- Replace the field placeholder, values and submission callback with the
  project's form contract and accessible adapters.
- Read the selected React Hook Form and Zod rules before adapting the example;
  they remain the canonical owners of form lifecycle and validation behavior.

## Checklist

- [ ] Defaults and values use the owning form contract.
- [ ] The resolver uses the matching runtime schema.
- [ ] Pending, invalid and failure states are visible to the user.
- [ ] Submission and close behavior follow local UI policy.
