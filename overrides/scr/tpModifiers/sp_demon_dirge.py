from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Demon Dirge"

def demonDirgeSpellOnBeginRound(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellDamageDice = dice_new('1d6')
    spellDamageDice.number = 2
    game.create_history_freeform("{} is affected by ~Demon Dirge~[TAG_SPELLS_DEMON_DIRGE]\n\n".format(attachee.description))
    attachee.float_text_line("Demon Dirge", tf_red)
    game.particles('hit-HOLY-medium', attachee)
    attachee.spell_damage(spellPacket.caster, D20DT_MAGIC, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0))
    return 0

def demonDirgeSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Demon Dirge ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Demon Dirge ({} rounds)".format(args.get_arg(1)))
    return 0

def demonDirgeSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("DEMON_DIRGE"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("DEMON_DIRGE"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def demonDirgeSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def demonDirgeSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def demonDirgeSpellSpellEnd(attachee, args, evt_obj):
    print "Demon Dirge SpellEnd"
    return 0

demonDirgeSpell = PythonModifier("sp-Demon Dirge", 2) # spell_id, duration
demonDirgeSpell.AddHook(ET_OnBeginRound, EK_NONE, demonDirgeSpellOnBeginRound, ())
demonDirgeSpell.AddHook(ET_OnGetTooltip, EK_NONE, demonDirgeSpellTooltip, ())
demonDirgeSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, demonDirgeSpellEffectTooltip, ())
demonDirgeSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, demonDirgeSpellSpellEnd, ())
demonDirgeSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, demonDirgeSpellHasSpellActive, ())
demonDirgeSpell.AddHook(ET_OnD20Signal, EK_S_Killed, demonDirgeSpellKilled, ())
demonDirgeSpell.AddSpellDispelCheckStandard()
demonDirgeSpell.AddSpellTeleportPrepareStandard()
demonDirgeSpell.AddSpellTeleportReconnectStandard()
demonDirgeSpell.AddSpellCountdownStandardHook()
