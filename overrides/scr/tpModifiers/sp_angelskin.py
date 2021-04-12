from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Angelskin"

def angelskinSpellEvilDr(attachee, args, evt_obj): 
    evt_obj.damage_packet.add_physical_damage_res(5, D20DAP_UNHOLY, 126) #Angelskin grants DR 5/evil; ID126 in damage.mes is DR
    return 0

def angelskinSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Angelskin ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Angelskin ({} rounds)".format(args.get_arg(1)))
    return 0

def angelskinSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("ANGELSKIN"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("ANGELSKIN"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def angelskinSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def angelskinSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def angelskinSpellSpellEnd(attachee, args, evt_obj):
    print "Angelskin SpellEnd"
    return 0

angelskinSpell = PythonModifier("sp-Angelskin", 2) # spell_id, duration
angelskinSpell.AddHook(ET_OnTakingDamage , EK_NONE, angelskinSpellEvilDr,())
angelskinSpell.AddHook(ET_OnGetTooltip, EK_NONE, angelskinSpellTooltip, ())
angelskinSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, angelskinSpellEffectTooltip, ())
angelskinSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, angelskinSpellSpellEnd, ())
angelskinSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, angelskinSpellHasSpellActive, ())
angelskinSpell.AddHook(ET_OnD20Signal, EK_S_Killed, angelskinSpellKilled, ())
angelskinSpell.AddSpellDispelCheckStandard()
angelskinSpell.AddSpellTeleportPrepareStandard()
angelskinSpell.AddSpellTeleportReconnectStandard()
angelskinSpell.AddSpellCountdownStandardHook()
