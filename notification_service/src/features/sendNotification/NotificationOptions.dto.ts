import {IsBooleanString, IsEmail, IsOptional, IsPhoneNumber} from "class-validator";
import {DTO} from '@/interfaces/DTO';

export class NotificationOptionsDto implements DTO {
    @IsOptional()
    @IsEmail()
    email: string;

    @IsOptional()
    @IsPhoneNumber()
    phoneNumber: number;

    @IsOptional()
    @IsBooleanString()
    persist: boolean;
}