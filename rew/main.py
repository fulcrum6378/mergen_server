import dat.search as search
import dat.config as cfg


def do_communicate():
    rewards = search.folders(cfg.root + "rew/")
    return len(rewards) > 0
