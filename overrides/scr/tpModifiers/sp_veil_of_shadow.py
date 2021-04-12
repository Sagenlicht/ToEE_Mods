from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Veil of Shadow"

def veilOfShadowSpellConcealment(attachee, args, evt_obj):
    evt_obj.bonus_list.add(20,0,"~Veil of Shadow~[TAG_SPELLS_VEIL_OF_SHADOW] Concealment Bonus") #Veil of Shadow grants 20% Concealment
    return 0

def veilOfShadowSpellCheckIfDaylight(attachee, args, evt_obj): #Veil of Shadow is dispelled by daylight
    checkOutdoor = game.is_outdoor()
    dayTime = game.time.time_game_in_hours(game.time)
    if dayTime in range(6,18): #includes 6 excludes 18
        daylightDispel = True
    else:
        daylightDispel = False

    if checkOutdoor and daylightDispel:
        attachee.float_text_line("Dispelled by daylight")
        args.set_arg(1, -1)
    return 0

def veilOfShadowSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Veil of Shadow (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append("Veil of Shadow (" + str(args.get_arg(1)) + " rounds)")
    return 0

def veilOfShadowSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("VEIL_OF_SHADOW"), -2, " (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append(tpdp.hash("VEIL_OF_SHADOW"), -2, " (" + str(args.get_arg(1)) + " rounds)")
    return 0

def veilOfShadowSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def veilOfShadowSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def veilOfShadowSpellSpellEnd(attachee, args, evt_obj):
    print "Veil of Shadow SpellEnd"
    return 0

veilOfShadowSpell = PythonModifier("sp-Veil of Shadow", 2) # spell_id, duration
veilOfShadowSpell.AddHook(ET_OnBeginRound, EK_NONE, veilOfShadowSpellCheckIfDaylight,())
veilOfShadowSpell.AddHook(ET_OnGetDefenderConcealmentMissChance, EK_NONE, veilOfShadowSpellConcealment,())
veilOfShadowSpell.AddHook(ET_OnGetTooltip, EK_NONE, veilOfShadowSpellTooltip, ())
veilOfShadowSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, veilOfShadowSpellEffectTooltip, ())
veilOfShadowSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, veilOfShadowSpellSpellEnd, ())
veilOfShadowSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, veilOfShadowSpellHasSpellActive, ())
veilOfShadowSpell.AddHook(ET_OnD20Signal, EK_S_Killed, veilOfShadowSpellKilled, ())
veilOfShadowSpell.AddSpellDispelCheckStandard()
veilOfShadowSpell.AddSpellTeleportPrepareStandard()
veilOfShadowSpell.AddSpellTeleportReconnectStandard()
veilOfShadowSpell.AddSpellCountdownStandardHook()
