from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Allegro"

def allegroSpellMovementBonus(attachee, args, evt_obj):
    moveSpeedBase = attachee.stat_level_get(stat_movement_speed)
    evt_obj.bonus_list.add(min(moveSpeedBase, 30), 12 ,"~Allegro~[TAG_SPELLS_ALLEGRO] ~Enhancement~[TAG_ENHANCEMENT_BONUS] Bonus") #Allegro adds 30ft. to movement speed, but is capped at double original speed.
    return 0


def allegroSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Allegro ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Allegro ({} rounds)".format(args.get_arg(1)))
    return 0

def allegroSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("ALLEGRO"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("ALLEGRO"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def allegroSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def allegroSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def allegroSpellSpellEnd(attachee, args, evt_obj):
    print "Allegro SpellEnd"
    return 0

allegroSpell = PythonModifier("sp-Allegro", 2) # spell_id, duration
allegroSpell.AddHook(ET_OnGetMoveSpeedBase, EK_NONE, allegroSpellMovementBonus,())
allegroSpell.AddHook(ET_OnGetTooltip, EK_NONE, allegroSpellTooltip, ())
allegroSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, allegroSpellEffectTooltip, ())
allegroSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, allegroSpellSpellEnd, ())
allegroSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, allegroSpellHasSpellActive, ())
allegroSpell.AddHook(ET_OnD20Signal, EK_S_Killed, allegroSpellKilled, ())
allegroSpell.AddSpellDispelCheckStandard()
allegroSpell.AddSpellTeleportPrepareStandard()
allegroSpell.AddSpellTeleportReconnectStandard()
allegroSpell.AddSpellCountdownStandardHook()
