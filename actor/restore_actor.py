from actor.actor import Actor

from actor.potion import Potion
from actor.fireball_scroll import FireballScroll
from actor.orc import Orc
from actor.troll import Troll
from actor.lightning_scroll import LightningScroll


def restore_actor(actor_dict):
    actor_name = list(actor_dict.keys())[0]

    if actor_name == "Actor":
        actor = Actor()
    elif actor_name == "Potion":
        actor = Potion()
    elif actor_name == "FireballScroll":
        actor = FireballScroll()
    elif actor_name == "LightningScroll":
        actor = LightningScroll()
    elif actor_name == "Orc":
        actor = Orc()
    elif actor_name == "Troll":
        actor = Troll()
    else:
        raise ValueError(f"Error, don't know how to restore {actor_name}.")

    actor.restore_from_dict(actor_dict[actor_name])

    return actor
