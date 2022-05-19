import {NotificationOptionsDto} from "@/features/sendNotification/NotificationOptions.dto";
import {IsOptional, IsString, ValidateNested} from "class-validator";
import {DTO} from "@/interfaces/DTO";


export class NotificationDto implements DTO {

    @IsString()
    text: string;

    @IsString()
    uid: string;

    @IsOptional()
    @ValidateNested()
    options: NotificationOptionsDto;
}