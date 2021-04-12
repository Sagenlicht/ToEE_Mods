from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Bladeweave"

def bladeweaveSpellBeginRound(attachee, args, evt_obj):
    args.set_arg(3, 0) #unset usedFlag
    return 0

def bladeweaveSpellChargeDamageBonus(attachee, args, evt_obj):
    target = evt_obj.attack_packet.target
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if not args.get_arg(3):
        if spellPacket.check_spell_resistance(target): #check spell resistance
            args.set_arg(3, 1)
            return 0
        #Saving throw to avoid dazed condition
        game.create_history_freeform(target.description + " saves versus ~Dazed~[TAG_DAZED] effect\n\n")
        if target.saving_throw_spell(args.get_arg(2), D20_Save_Will, D20STD_F_NONE, spellPacket.caster, args.get_arg(0)): #success
            target.float_text_line("Not Dazed")
        else:
            target.condition_add('Dazed Condition', 1)
        args.set_arg(3, 1)
    return 0

def bladeweaveSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Bladeweave ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Bladeweave ({} rounds)".format(args.get_arg(1)))
    return 0

def bladeweaveSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("WAR_CRY"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("WAR_CRY"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def bladeweaveSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def bladeweaveSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def bladeweaveSpellSpellEnd(attachee, args, evt_obj):
    print "BladeweaveSpellEnd"
    return 0

bladeweaveSpell = PythonModifier("sp-Bladeweave", 5) # spell_id, duration, spellDc, usedFlag
bladeweaveSpell.AddHook(ET_OnBeginRound, EK_NONE, bladeweaveSpellBeginRound,())
bladeweaveSpell.AddHook(ET_OnDealingDamage, EK_NONE, bladeweaveSpellChargeDamageBonus,())
bladeweaveSpell.AddHook(ET_OnGetTooltip, EK_NONE, bladeweaveSpellTooltip, ())
bladeweaveSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, bladeweaveSpellEffectTooltip, ())
bladeweaveSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, bladeweaveSpellSpellEnd, ())
bladeweaveSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, bladeweaveSpellHasSpellActive, ())
bladeweaveSpell.AddHook(ET_OnD20Signal, EK_S_Killed, bladeweaveSpellKilled, ())
bladeweaveSpell.AddSpellDispelCheckStandard()
bladeweaveSpell.AddSpellTeleportPrepareStandard()
bladeweaveSpell.AddSpellTeleportReconnectStandard()
bladeweaveSpell.AddSpellCountdownStandardHook()
