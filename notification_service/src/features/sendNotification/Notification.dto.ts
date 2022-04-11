import {NotificationOptionsDto} from "@/features/sendNotification/NotificationOptions.dto";
import {IsNumberString, IsOptional, IsString, ValidateNested} from "class-validator";
import {DTO} from "@/interfaces/DTO";


export class NotificationDto implements DTO {

    @IsString()
    text: string;

    @IsNumberString()
    uid: number;

    @IsOptional()
    @ValidateNested()
    options: NotificationOptionsDto;
}