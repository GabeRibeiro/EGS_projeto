import {DTO} from "@/interfaces/DTO";
import {IsNumberString, IsOptional, Min, ValidateIf} from "class-validator";

export class PaginationDto implements DTO {
    @IsOptional()
    @IsNumberString()
    @Min(1)
    nrPage: number;

    @ValidateIf(o => o.nrPage)
    @IsNumberString()
    @Min(1)
    resultsPerPage: number;
}