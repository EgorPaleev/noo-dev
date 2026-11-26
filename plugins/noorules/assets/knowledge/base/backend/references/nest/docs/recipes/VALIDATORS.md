# Кастомные class-validator constraint'ы

**Паттерн на будущее**: пример `Match` ниже — готовый рецепт на случай, когда понадобится cross-field валидация; в коде пока не заведён ни один кастомный constraint.

Когда нужна валидация, зависящая сразу от нескольких полей DTO (например, `password`/`passwordConfirm` должны совпадать) — `registerDecorator` из `class-validator`, а не ручная проверка в сервисе. Применимо к любому DTO, не только auth-related.

```ts
export function Match(property: string, validationOptions?: ValidationOptions)
{
    return (object: any, propertyName: string) =>
    {
        registerDecorator({
            name: "Match",
            target: object.constructor,
            propertyName,
            options: validationOptions,
            constraints: [property],
            validator: {
                validate(value: any, args: ValidationArguments)
                {
                    const [relatedPropertyName] = args.constraints;
                    return value === (args.object as any)[relatedPropertyName];
                },
                defaultMessage(args: ValidationArguments)
                {
                    const [relatedPropertyName] = args.constraints;
                    return `Поле "${args.property}" должно совпадать с полем "${relatedPropertyName}"`;
                },
            },
        });
    };
}

// dto
@Match("password", { message: "Пароли не совпадают" })
passwordConfirm: string;
```
