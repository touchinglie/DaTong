import logging

basicFormatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
)

def getLogger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    return logger

def getLogHandle(name: str, fileOrNot: bool) -> logging.Handler:
    if fileOrNot:
        handler = logging.FileHandler(f"{name}.log")
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(basicFormatter)
    return handler

def enableDebugOrNot(enable:bool) -> None:
    if not enable:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        return
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return
