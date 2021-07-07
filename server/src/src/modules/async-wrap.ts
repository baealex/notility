import {
    Request,
    Response,
    NextFunction,
} from 'express'

export default function asyncWrap(callback: any) {
    return function (req: Request, res: Response, next: NextFunction) {
        callback(req, res, next)
            .catch((e: Error) => {
                console.log(e);
                next();
            })
    }
}