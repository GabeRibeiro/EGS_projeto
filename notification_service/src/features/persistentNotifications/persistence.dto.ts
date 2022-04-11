import {DTO} from "@/interfaces/DTO";
import {IsNumberString, IsOptional} from "class-validator";

export class PersistenceDto implements DTO {
    @IsOptional()
    @IsNumberString()
    page: number;

    @IsOptional()
    @IsNumberString()
    nrPerPage: number;
}