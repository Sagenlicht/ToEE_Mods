from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-War Cry"

def warCrySpellChargeAttackBonus(attachee, args, evt_obj):
    if evt_obj.attack_packet.get_flags() & D20CAF_CHARGE:
        evt_obj.bonus_list.add(4,13,"~War Cry~[TAG_SPELLS_WAR_CRY] ~Morale~[TAG_MODIFIER_MORALE] Bonus") #War Cry is a +4 Morale Bonus to Attack Rolls while charging
    return 0

def warCrySpellChargeDamageBonus(attachee, args, evt_obj):
    target = evt_obj.attack_packet.target
    spellPacket = tpdp.SpellPacket(args.get_arg(0))

    if evt_obj.attack_packet.get_flags() & D20CAF_CHARGE:
        evt_obj.damage_packet.bonus_list.add(4, 13, "~War Cry~[TAG_SPELLS_WAR_CRY] ~Morale~[TAG_MODIFIER_MORALE] Bonus")
        #Saving throw to avoid panicked condition; racial immunity is checked in the condition itself
        game.create_history_freeform(attachee.description + " saves versus ~War Cry~[TAG_SPELLS_WAR_CRY] panicked effect\n\n")
        if target.saving_throw_spell(args.get_arg(2), D20_Save_Will, D20STD_F_NONE, spellPacket.caster, args.get_arg(0)): #success
            target.float_text_line("Not Panicked")
        else:
            target.condition_add('Panicked Condition', 1, spellPacket.spell_id)
    return 0

def warCrySpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("War Cry (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append("War Cry (" + str(args.get_arg(1)) + " rounds)")
    return 0

def warCrySpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("WAR_CRY"), -2, " (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append(tpdp.hash("WAR_CRY"), -2, " (" + str(args.get_arg(1)) + " rounds)")
    return 0

def warCrySpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def warCrySpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def warCrySpellSpellEnd(attachee, args, evt_obj):
    print "War CrySpellEnd"
    return 0

warCrySpell = PythonModifier("sp-War Cry", 3) # spell_id, duration, spellDc
warCrySpell.AddHook(ET_OnToHitBonus2, EK_NONE, warCrySpellChargeAttackBonus,())
warCrySpell.AddHook(ET_OnDealingDamage, EK_NONE, warCrySpellChargeDamageBonus,())
warCrySpell.AddHook(ET_OnGetTooltip, EK_NONE, warCrySpellTooltip, ())
warCrySpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, warCrySpellEffectTooltip, ())
warCrySpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, warCrySpellSpellEnd, ())
warCrySpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, warCrySpellHasSpellActive, ())
warCrySpell.AddHook(ET_OnD20Signal, EK_S_Killed, warCrySpellKilled, ())
warCrySpell.AddSpellDispelCheckStandard()
warCrySpell.AddSpellTeleportPrepareStandard()
warCrySpell.AddSpellTeleportReconnectStandard()
warCrySpell.AddSpellCountdownStandardHook()
